package com.schemesathi.auth;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Audit record of a user login session for the admin dashboard.
 */
public class LoginRecord {
    private final String id;
    private final String username;
    private final String email;
    private final String role;
    private final String timestamp;
    private final String ipAddress;
    private final String status; // "SUCCESS" or "FAILED"

    public LoginRecord(String id, String username, String email, String role, String ipAddress, String status) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.role = role;
        this.timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
        this.ipAddress = ipAddress != null ? ipAddress : "127.0.0.1";
        this.status = status;
    }

    public String getId() {
        return id;
    }

    public String getUsername() {
        return username;
    }

    public String getEmail() {
        return email;
    }

    public String getRole() {
        return role;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public String getIpAddress() {
        return ipAddress;
    }

    public String getStatus() {
        return status;
    }
}
