package com.schemesathi.auth;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class AuthServiceTest {

    private AuthService authService;

    @BeforeEach
    void setUp() {
        authService = new AuthService();
    }

    @Test
    @DisplayName("Default seeded admin can log in and receives session token")
    void testAdminLogin() {
        Map<String, Object> result = authService.login("admin", "Admin@123", "127.0.0.1");
        assertNotNull(result);
        assertTrue(result.containsKey("token"));
        assertEquals("admin", result.get("username"));
        assertEquals("ADMIN", result.get("role"));

        String token = (String) result.get("token");
        User user = authService.validateSession(token);
        assertNotNull(user);
        assertTrue(user.isAdmin());
    }

    @Test
    @DisplayName("Invalid password throws IllegalArgumentException")
    void testInvalidPassword() {
        assertThrows(IllegalArgumentException.class, () -> authService.login("admin", "WrongPass", "127.0.0.1"));
    }

    @Test
    @DisplayName("New user registration and subsequent login succeed")
    void testUserRegistrationAndLogin() {
        User newUser = authService.register("priya_patel", "priya@example.com", "Password@123", "STUDENT");
        assertEquals("priya_patel", newUser.getUsername());
        assertEquals("STUDENT", newUser.getRole());

        Map<String, Object> login = authService.login("priya@example.com", "Password@123", "10.0.0.1");
        assertNotNull(login.get("token"));
        assertEquals("STUDENT", login.get("role"));
    }

    @Test
    @DisplayName("Admin can view login records and non-admin is forbidden")
    void testAdminLoginsAndAccessControl() {
        Map<String, Object> adminLogin = authService.login("admin", "Admin@123", "127.0.0.1");
        String adminToken = (String) adminLogin.get("token");

        List<LoginRecord> records = authService.getLoginHistory(adminToken);
        assertFalse(records.isEmpty());

        // Register student and verify student cannot fetch audit logs
        User student = authService.register("student1", "s1@example.com", "Secret123", "STUDENT");
        Map<String, Object> studentLogin = authService.login("student1", "Secret123", "127.0.0.1");
        String studentToken = (String) studentLogin.get("token");

        assertThrows(SecurityException.class, () -> authService.getLoginHistory(studentToken));
    }

    @Test
    @DisplayName("Admin can export login records as CSV")
    void testCsvExport() {
        Map<String, Object> adminLogin = authService.login("admin", "Admin@123", "127.0.0.1");
        String adminToken = (String) adminLogin.get("token");

        String csv = authService.generateCsv(adminToken);
        assertNotNull(csv);
        assertTrue(csv.contains("Log ID,Username,Email,Role,Timestamp,IP Address,Status"));
        assertTrue(csv.contains("admin"));
    }
}
