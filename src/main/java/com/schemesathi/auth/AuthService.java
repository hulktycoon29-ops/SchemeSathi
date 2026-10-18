package com.schemesathi.auth;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.regex.Pattern;

/**
 * Service managing user authentication, secure credential hashing,
 * session token issuance, and login session auditing for the admin console.
 */
public class AuthService {
    private static final Pattern EMAIL_PATTERN = Pattern.compile("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$");
    private final Map<String, User> usersByUsername = new ConcurrentHashMap<>();
    private final Map<String, User> usersByEmail = new ConcurrentHashMap<>();
    private final Map<String, User> activeSessions = new ConcurrentHashMap<>();
    private final List<LoginRecord> loginHistory = new CopyOnWriteArrayList<>();
    private final SecureRandom secureRandom = new SecureRandom();

    public AuthService() {
        // Seed initial administrator account
        registerInternal("Priyanshu", "admin@schemesathi.gov", "Pg@12345", "ADMIN");
        // Seed a sample registered student
        registerInternal("rahul_sharma", "rahul.sharma@example.com", "Student@123", "STUDENT");

        // Seed initial audit log for demo visualization
        loginHistory.add(new LoginRecord("LOG-" + UUID.randomUUID().toString().substring(0, 8),
                "admin", "admin@schemesathi.gov", "ADMIN", "127.0.0.1", "SUCCESS"));
        loginHistory.add(new LoginRecord("LOG-" + UUID.randomUUID().toString().substring(0, 8),
                "rahul_sharma", "rahul.sharma@example.com", "STUDENT", "192.168.1.15", "SUCCESS"));
    }

    private User registerInternal(String username, String email, String password, String role) {
        String salt = generateSalt();
        String hash = hashPassword(password, salt);
        User user = new User("USR-" + UUID.randomUUID().toString().substring(0, 8),
                username.trim().toLowerCase(),
                email.trim().toLowerCase(),
                hash,
                salt,
                role);
        usersByUsername.put(user.getUsername(), user);
        usersByEmail.put(user.getEmail(), user);
        return user;
    }

    public User register(String username, String email, String password, String role) {
        if (username == null || username.trim().length() < 3) {
            throw new IllegalArgumentException("Username must be at least 3 characters.");
        }
        if (email == null || !EMAIL_PATTERN.matcher(email.trim()).matches()) {
            throw new IllegalArgumentException("A valid email address is required.");
        }
        if (password == null || password.length() < 6) {
            throw new IllegalArgumentException("Password must be at least 6 characters.");
        }

        String normalizedUsername = username.trim().toLowerCase();
        String normalizedEmail = email.trim().toLowerCase();

        if (usersByUsername.containsKey(normalizedUsername)) {
            throw new IllegalArgumentException("Username '" + username + "' is already taken.");
        }
        if (usersByEmail.containsKey(normalizedEmail)) {
            throw new IllegalArgumentException("Email '" + email + "' is already registered.");
        }

        String assignedRole = "admin".equalsIgnoreCase(role) ? "ADMIN" : "STUDENT";
        return registerInternal(normalizedUsername, normalizedEmail, password, assignedRole);
    }

    public Map<String, Object> login(String usernameOrEmail, String password, String ipAddress) {
        if (usernameOrEmail == null || usernameOrEmail.trim().isEmpty()) {
            throw new IllegalArgumentException("Username or email is required.");
        }
        if (password == null || password.isEmpty()) {
            throw new IllegalArgumentException("Password is required.");
        }

        String query = usernameOrEmail.trim().toLowerCase();
        User user = usersByUsername.get(query);
        if (user == null) {
            user = usersByEmail.get(query);
        }

        if (user == null) {
            recordLoginAttempt(query, query.contains("@") ? query : "unknown", "UNKNOWN", ipAddress, "FAILED");
            throw new IllegalArgumentException("Invalid username/email or password.");
        }

        String expectedHash = hashPassword(password, user.getSalt());
        if (!expectedHash.equals(user.getPasswordHash())) {
            recordLoginAttempt(user.getUsername(), user.getEmail(), user.getRole(), ipAddress, "FAILED");
            throw new IllegalArgumentException("Invalid username/email or password.");
        }

        // Successful login
        String sessionToken = "STOK-" + UUID.randomUUID().toString().replace("-", "")
                + Long.toHexString(System.currentTimeMillis());
        activeSessions.put(sessionToken, user);

        LoginRecord record = recordLoginAttempt(user.getUsername(), user.getEmail(), user.getRole(), ipAddress,
                "SUCCESS");

        Map<String, Object> result = new LinkedHashMap<>();
        result.put("token", sessionToken);
        result.put("username", user.getUsername());
        result.put("email", user.getEmail());
        result.put("role", user.getRole());
        result.put("loginId", record.getId());
        result.put("timestamp", record.getTimestamp());
        return result;
    }

    public User validateSession(String token) {
        if (token == null || token.trim().isEmpty()) {
            return null;
        }
        // Support Bearer token prefix if provided
        String cleanToken = token.startsWith("Bearer ") ? token.substring(7).trim() : token.trim();
        return activeSessions.get(cleanToken);
    }

    public List<LoginRecord> getLoginHistory(String token) {
        User user = validateSession(token);
        if (user == null) {
            throw new SecurityException("Unauthorized: Valid session token is required.");
        }
        if (!user.isAdmin()) {
            throw new SecurityException("Forbidden: Only administrators can access login records.");
        }
        // Return latest first
        List<LoginRecord> copy = new ArrayList<>(loginHistory);
        Collections.reverse(copy);
        return copy;
    }

    public String generateCsv(String token) {
        List<LoginRecord> records = getLoginHistory(token);
        StringBuilder sb = new StringBuilder();
        // UTF-8 BOM for Excel compatibility
        sb.append('\ufeff');
        sb.append("Log ID,Username,Email,Role,Timestamp,IP Address,Status\r\n");

        for (LoginRecord r : records) {
            sb.append(escapeCsv(r.getId())).append(',')
                    .append(escapeCsv(r.getUsername())).append(',')
                    .append(escapeCsv(r.getEmail())).append(',')
                    .append(escapeCsv(r.getRole())).append(',')
                    .append(escapeCsv(r.getTimestamp())).append(',')
                    .append(escapeCsv(r.getIpAddress())).append(',')
                    .append(escapeCsv(r.getStatus())).append("\r\n");
        }
        return sb.toString();
    }

    private LoginRecord recordLoginAttempt(String username, String email, String role, String ipAddress,
            String status) {
        String logId = "LOG-" + UUID.randomUUID().toString().substring(0, 8);
        LoginRecord record = new LoginRecord(logId, username, email, role, ipAddress, status);
        loginHistory.add(record);
        return record;
    }

    private String generateSalt() {
        byte[] saltBytes = new byte[16];
        secureRandom.nextBytes(saltBytes);
        return HexFormat.of().formatHex(saltBytes);
    }

    private String hashPassword(String password, String salt) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            digest.update(salt.getBytes(StandardCharsets.UTF_8));
            byte[] hash = digest.digest(password.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().formatHex(hash);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 algorithm missing", e);
        }
    }

    private String escapeCsv(String value) {
        if (value == null)
            return "\"\"";
        if (value.contains(",") || value.contains("\"") || value.contains("\n") || value.contains("\r")) {
            return "\"" + value.replace("\"", "\"\"") + "\"";
        }
        return "\"" + value + "\"";
    }
}
