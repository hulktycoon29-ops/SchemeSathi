package com.schemesathi.auth;

import java.time.Instant;

/**
 * Represents a registered user in SchemeSathi.
 */
public class User {
    private final String id;
    private final String username;
    private final String email;
    private final String passwordHash;
    private final String salt;
    private final String role; // "ADMIN" or "STUDENT"
    private final Instant createdAt;

    public User(String id, String username, String email, String passwordHash, String salt, String role) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.passwordHash = passwordHash;
        this.salt = salt;
        this.role = role != null ? role.toUpperCase() : "STUDENT";
        this.createdAt = Instant.now();
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

    public String getPasswordHash() {
        return passwordHash;
    }

    public String getSalt() {
        return salt;
    }

    public String getRole() {
        return role;
    }

    public boolean isAdmin() {
        return "ADMIN".equalsIgnoreCase(role);
    }

    public Instant getCreatedAt() {
        return createdAt;
    }
}
