package com.schemesathi.server;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import com.schemesathi.loader.SchemeLoader;
import com.schemesathi.model.CategoryScheme;
import com.schemesathi.model.IncomeScheme;
import com.schemesathi.model.MeritScheme;
import com.schemesathi.model.Scheme;
import com.schemesathi.model.Student;
import com.schemesathi.report.EligibilityReportWriter;
import com.schemesathi.service.EligibilityService;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.concurrent.Executors;

/**
 * High-performance, lightweight REST API server built directly with standard Java HttpServer.
 * Directly integrates with SchemeSathi domain models, SchemeLoader, and EligibilityService.
 */
import com.schemesathi.auth.AuthService;
import com.schemesathi.auth.LoginRecord;
import com.schemesathi.auth.User;

public class ApiServer {
    private final int port;
    private final SchemeLoader schemeLoader;
    private final EligibilityService eligibilityService;
    private final EligibilityReportWriter reportWriter;
    private final AuthService authService;
    private final ObjectMapper objectMapper;
    private HttpServer server;

    public ApiServer(int port) {
        this.port = port;
        this.schemeLoader = new SchemeLoader();
        this.eligibilityService = new EligibilityService();
        this.reportWriter = new EligibilityReportWriter();
        this.authService = new AuthService();
        this.objectMapper = new ObjectMapper();
    }

    public void start() throws IOException {
        server = HttpServer.create(new InetSocketAddress(port), 0);
        server.setExecutor(Executors.newFixedThreadPool(16));

        // Endpoints
        server.createContext("/", new RootHandler());
        server.createContext("/api/health", new HealthHandler());
        server.createContext("/api/schemes", new SchemesHandler());
        server.createContext("/api/evaluate", new EvaluateHandler());
        server.createContext("/api/report", new ReportHandler());
        server.createContext("/api/auth/register", new RegisterHandler());
        server.createContext("/api/auth/login", new LoginHandler());
        server.createContext("/api/auth/me", new MeHandler());
        server.createContext("/api/admin/logins", new AdminLoginsHandler());
        server.createContext("/api/admin/logins/csv", new AdminCsvHandler());

        server.start();
        System.out.println("==================================================================");
        System.out.println(" [✓] SchemeSathi Backend REST API Server is RUNNING on port " + port);
        System.out.println("     Health check:  http://localhost:" + port + "/api/health");
        System.out.println("     Schemes API:   http://localhost:" + port + "/api/schemes");
        System.out.println("     Evaluate API:  http://localhost:" + port + "/api/evaluate");
        System.out.println("     Auth & Login:  http://localhost:" + port + "/api/auth/login");
        System.out.println("     Admin Console: http://localhost:" + port + "/api/admin/logins");
        System.out.println("==================================================================");
    }

    public void stop() {
        if (server != null) {
            server.stop(0);
            System.out.println("ApiServer stopped.");
        }
    }

    private Path getRulesPath() {
        Path p = Path.of("data", "schemes.json");
        if (Files.exists(p)) return p;
        p = Path.of("..", "data", "schemes.json");
        return p;
    }

    private void addCorsHeaders(HttpExchange exchange) {
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        exchange.getResponseHeaders().set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
        exchange.getResponseHeaders().set("Access-Control-Allow-Headers", "Content-Type, Authorization");
    }

    private void sendJsonResponse(HttpExchange exchange, int statusCode, Object data) throws IOException {
        addCorsHeaders(exchange);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        byte[] bytes = objectMapper.writeValueAsBytes(data);
        exchange.sendResponseHeaders(statusCode, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(bytes);
        }
    }

    private Map<String, Object> mapScheme(Scheme s) {
        Map<String, Object> map = new LinkedHashMap<>();
        map.put("id", s.getId());
        map.put("name", s.getName());
        map.put("type", s.getType());
        map.put("criteriaSummary", s.getCriteriaSummary());
        map.put("requiredDocuments", s.getRequiredDocuments());

        if (s instanceof MeritScheme ms) {
            map.put("minimumMarks", ms.getMinimumMarks());
        } else if (s instanceof IncomeScheme is) {
            map.put("maximumAnnualIncome", is.getMaximumAnnualIncome());
        } else if (s instanceof CategoryScheme cs) {
            map.put("allowedCategories", cs.getAllowedCategories());
        }
        return map;
    }

    // Root Handler
    private class RootHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            addCorsHeaders(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            Map<String, Object> res = new LinkedHashMap<>();
            res.put("status", "UP");
            res.put("application", "SchemeSathi Java Backend REST API Server");
            res.put("healthCheck", "/api/health");
            res.put("schemesApi", "/api/schemes");
            res.put("loginApi", "/api/auth/login");
            res.put("message", "SchemeSathi Backend is operational. Access the web interface on your frontend URL.");
            sendJsonResponse(exchange, 200, res);
        }
    }

    // Health Handler
    private class HealthHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            addCorsHeaders(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            Map<String, Object> res = new HashMap<>();
            res.put("status", "UP");
            res.put("application", "SchemeSathi Scholarship Navigator");
            res.put("version", "1.0.0");
            res.put("runtime", System.getProperty("java.version"));
            sendJsonResponse(exchange, 200, res);
        }
    }

    // Schemes Handler
    private class SchemesHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            addCorsHeaders(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            try {
                List<Scheme> list = schemeLoader.load(getRulesPath());
                List<Map<String, Object>> res = new ArrayList<>();
                for (Scheme s : list) {
                    res.add(mapScheme(s));
                }
                sendJsonResponse(exchange, 200, Map.of(
                        "success", true,
                        "count", res.size(),
                        "schemes", res
                ));
            } catch (Exception e) {
                sendJsonResponse(exchange, 500, Map.of(
                        "success", false,
                        "error", e.getMessage()
                ));
            }
        }
    }

    // Evaluate Handler
    private class EvaluateHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            addCorsHeaders(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }

            if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                sendJsonResponse(exchange, 405, Map.of("success", false, "error", "Method not allowed. Use POST."));
                return;
            }

            try (InputStream is = exchange.getRequestBody()) {
                Map<String, Object> body = objectMapper.readValue(is, new com.fasterxml.jackson.core.type.TypeReference<Map<String, Object>>() {});

                Object marksObj = body.get("marks");
                Object incomeObj = body.get("annualFamilyIncome");
                Object categoryObj = body.get("category");

                if (marksObj == null || incomeObj == null || categoryObj == null) {
                    sendJsonResponse(exchange, 400, Map.of(
                            "success", false,
                            "error", "Missing required fields: marks, annualFamilyIncome, category"
                    ));
                    return;
                }

                double marks = Double.parseDouble(marksObj.toString());
                double income = Double.parseDouble(incomeObj.toString());
                String category = categoryObj.toString();

                Student student;
                try {
                    student = new Student(marks, income, category);
                } catch (IllegalArgumentException valEx) {
                    sendJsonResponse(exchange, 400, Map.of(
                            "success", false,
                            "error", valEx.getMessage()
                    ));
                    return;
                }

                List<Scheme> allSchemes = schemeLoader.load(getRulesPath());
                List<Scheme> eligible = eligibilityService.findEligible(student, allSchemes);

                List<Map<String, Object>> eligibleList = new ArrayList<>();
                for (Scheme s : eligible) {
                    eligibleList.add(mapScheme(s));
                }

                Map<String, Object> studentMap = new LinkedHashMap<>();
                studentMap.put("marks", student.getMarks());
                studentMap.put("annualFamilyIncome", student.getAnnualFamilyIncome());
                studentMap.put("category", student.getCategory());

                Map<String, Object> response = new LinkedHashMap<>();
                response.put("success", true);
                response.put("student", studentMap);
                response.put("totalSchemesEvaluated", allSchemes.size());
                response.put("matchedCount", eligible.size());
                response.put("eligibleSchemes", eligibleList);

                sendJsonResponse(exchange, 200, response);
            } catch (Exception e) {
                sendJsonResponse(exchange, 500, Map.of(
                        "success", false,
                        "error", e.getMessage()
                ));
            }
        }
    }

    // Report Handler
    private class ReportHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            addCorsHeaders(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }

            if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                sendJsonResponse(exchange, 405, Map.of("success", false, "error", "Method not allowed. Use POST."));
                return;
            }

            try (InputStream is = exchange.getRequestBody()) {
                Map<String, Object> body = objectMapper.readValue(is, new com.fasterxml.jackson.core.type.TypeReference<Map<String, Object>>() {});
                double marks = Double.parseDouble(body.get("marks").toString());
                double income = Double.parseDouble(body.get("annualFamilyIncome").toString());
                String category = body.get("category").toString();

                Student student = new Student(marks, income, category);
                List<Scheme> allSchemes = schemeLoader.load(getRulesPath());
                List<Scheme> eligible = eligibilityService.findEligible(student, allSchemes);

                Path reportPath = Path.of("output", "eligibility-report.txt");
                reportWriter.write(reportPath, student, eligible);

                String reportText = Files.readString(reportPath, StandardCharsets.UTF_8);

                sendJsonResponse(exchange, 200, Map.of(
                        "success", true,
                        "filePath", reportPath.toAbsolutePath().toString(),
                        "reportContent", reportText
                ));
            } catch (Exception e) {
                sendJsonResponse(exchange, 500, Map.of(
                        "success", false,
                        "error", e.getMessage()
                ));
            }
        }
    }

    private String extractToken(HttpExchange exchange) {
        String authHeader = exchange.getRequestHeaders().getFirst("Authorization");
        if (authHeader != null && !authHeader.trim().isEmpty()) {
            if (authHeader.startsWith("Bearer ")) {
                return authHeader.substring(7).trim();
            }
            return authHeader.trim();
        }
        String query = exchange.getRequestURI().getQuery();
        if (query != null) {
            for (String param : query.split("&")) {
                String[] pair = param.split("=");
                if (pair.length == 2 && "token".equalsIgnoreCase(pair[0])) {
                    return pair[1].trim();
                }
            }
        }
        return null;
    }

    // Register Handler
    private class RegisterHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            addCorsHeaders(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }

            if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                sendJsonResponse(exchange, 405, Map.of("success", false, "error", "Method not allowed. Use POST."));
                return;
            }

            try (InputStream is = exchange.getRequestBody()) {
                Map<String, Object> body = objectMapper.readValue(is, new com.fasterxml.jackson.core.type.TypeReference<Map<String, Object>>() {});
                String username = body.get("username") != null ? body.get("username").toString() : null;
                String email = body.get("email") != null ? body.get("email").toString() : null;
                String password = body.get("password") != null ? body.get("password").toString() : null;
                String role = body.get("role") != null ? body.get("role").toString() : "STUDENT";

                User user = authService.register(username, email, password, role);
                String remoteIp = exchange.getRemoteAddress() != null ? exchange.getRemoteAddress().getAddress().getHostAddress() : "127.0.0.1";
                Map<String, Object> loginResult = authService.login(user.getUsername(), password, remoteIp);

                Map<String, Object> res = new LinkedHashMap<>();
                res.put("success", true);
                res.put("message", "User registered and authenticated successfully");
                res.putAll(loginResult);
                sendJsonResponse(exchange, 201, res);
            } catch (IllegalArgumentException iae) {
                sendJsonResponse(exchange, 400, Map.of("success", false, "error", iae.getMessage()));
            } catch (Exception e) {
                sendJsonResponse(exchange, 500, Map.of("success", false, "error", e.getMessage()));
            }
        }
    }

    // Login Handler
    private class LoginHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            addCorsHeaders(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }

            if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                sendJsonResponse(exchange, 405, Map.of("success", false, "error", "Method not allowed. Use POST."));
                return;
            }

            try (InputStream is = exchange.getRequestBody()) {
                Map<String, Object> body = objectMapper.readValue(is, new com.fasterxml.jackson.core.type.TypeReference<Map<String, Object>>() {});
                String usernameOrEmail = body.get("username") != null ? body.get("username").toString() :
                        (body.get("email") != null ? body.get("email").toString() : null);
                String password = body.get("password") != null ? body.get("password").toString() : null;

                String remoteIp = exchange.getRemoteAddress() != null ? exchange.getRemoteAddress().getAddress().getHostAddress() : "127.0.0.1";

                Map<String, Object> loginResult = authService.login(usernameOrEmail, password, remoteIp);
                Map<String, Object> res = new LinkedHashMap<>();
                res.put("success", true);
                res.putAll(loginResult);
                sendJsonResponse(exchange, 200, res);
            } catch (IllegalArgumentException iae) {
                sendJsonResponse(exchange, 401, Map.of("success", false, "error", iae.getMessage()));
            } catch (Exception e) {
                sendJsonResponse(exchange, 500, Map.of("success", false, "error", e.getMessage()));
            }
        }
    }

    // Current User Profile Handler
    private class MeHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            addCorsHeaders(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }

            String token = extractToken(exchange);
            User user = authService.validateSession(token);
            if (user == null) {
                sendJsonResponse(exchange, 401, Map.of("success", false, "error", "Invalid or expired session token."));
                return;
            }

            sendJsonResponse(exchange, 200, Map.of(
                    "success", true,
                    "user", Map.of(
                            "id", user.getId(),
                            "username", user.getUsername(),
                            "email", user.getEmail(),
                            "role", user.getRole()
                    )
            ));
        }
    }

    // Admin Logins List Handler
    private class AdminLoginsHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            addCorsHeaders(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }

            if (!"GET".equalsIgnoreCase(exchange.getRequestMethod())) {
                sendJsonResponse(exchange, 405, Map.of("success", false, "error", "Method not allowed. Use GET."));
                return;
            }

            String token = extractToken(exchange);
            try {
                List<LoginRecord> records = authService.getLoginHistory(token);
                sendJsonResponse(exchange, 200, Map.of(
                        "success", true,
                        "count", records.size(),
                        "logins", records
                ));
            } catch (SecurityException se) {
                sendJsonResponse(exchange, 403, Map.of("success", false, "error", se.getMessage()));
            } catch (Exception e) {
                sendJsonResponse(exchange, 500, Map.of("success", false, "error", e.getMessage()));
            }
        }
    }

    // Admin CSV Export Handler
    private class AdminCsvHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            addCorsHeaders(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }

            if (!"GET".equalsIgnoreCase(exchange.getRequestMethod())) {
                sendJsonResponse(exchange, 405, Map.of("success", false, "error", "Method not allowed. Use GET."));
                return;
            }

            String token = extractToken(exchange);
            try {
                String csvData = authService.generateCsv(token);
                byte[] bytes = csvData.getBytes(StandardCharsets.UTF_8);
                exchange.getResponseHeaders().set("Content-Type", "text/csv; charset=UTF-8");
                exchange.getResponseHeaders().set("Content-Disposition", "attachment; filename=\"schemesathi-logins.csv\"");
                exchange.sendResponseHeaders(200, bytes.length);
                try (OutputStream os = exchange.getResponseBody()) {
                    os.write(bytes);
                }
            } catch (SecurityException se) {
                sendJsonResponse(exchange, 403, Map.of("success", false, "error", se.getMessage()));
            } catch (Exception e) {
                sendJsonResponse(exchange, 500, Map.of("success", false, "error", e.getMessage()));
            }
        }
    }
}
