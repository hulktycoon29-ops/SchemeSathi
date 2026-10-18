package com.schemesathi;

import com.schemesathi.server.ApiServer;
import com.schemesathi.ui.ConsoleUI;

/**
 * Main application coordinator for SchemeSathi.
 * Supports running as an interactive console application (as required by PRD)
 * or as a robust backend REST API server (to power the modern Web UI).
 */
public class Main {
    public static void main(String[] args) {
        int port = 8080;
        String envPort = System.getenv("PORT");
        if (envPort != null && !envPort.trim().isEmpty()) {
            try {
                port = Integer.parseInt(envPort.trim());
            } catch (NumberFormatException ignored) {}
        }
        boolean runServer = false;
        boolean runCli = false;

        for (int i = 0; i < args.length; i++) {
            String arg = args[i];
            if ("--server".equalsIgnoreCase(arg) || "-s".equalsIgnoreCase(arg)) {
                runServer = true;
            } else if ("--cli".equalsIgnoreCase(arg) || "-c".equalsIgnoreCase(arg)) {
                runCli = true;
            } else if ("--port".equalsIgnoreCase(arg) && i + 1 < args.length) {
                try {
                    port = Integer.parseInt(args[++i]);
                } catch (NumberFormatException ignored) {}
            }
        }

        if (runServer && !runCli) {
            startServer(port);
            return;
        }

        if (runCli && !runServer) {
            new ConsoleUI().run();
            return;
        }

        // Default behavior when run without flags:
        // Start server in background so Web frontend works out-of-the-box,
        // and run the interactive CLI in foreground!
        System.out.println("==================================================================");
        System.out.println("      SchemeSathi — Scholarship Navigator (Console & Server)      ");
        System.out.println("==================================================================");
        System.out.println("Starting background REST API Server on port " + port + " for Web UI...");
        try {
            ApiServer apiServer = new ApiServer(port);
            apiServer.start();
            Runtime.getRuntime().addShutdownHook(new Thread(apiServer::stop));
        } catch (Exception e) {
            System.err.println("[!] Warning: Could not bind API server to port " + port + ": " + e.getMessage());
        }

        System.out.println("\nLaunching Interactive Console UI:\n");
        new ConsoleUI().run();
    }

    private static void startServer(int port) {
        try {
            ApiServer apiServer = new ApiServer(port);
            apiServer.start();
            System.out.println("Press Ctrl+C to stop the server.");
            Thread.currentThread().join();
        } catch (Exception e) {
            System.err.println("[X] Fatal: Failed to start API Server: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}
