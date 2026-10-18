# ==========================================
# SchemeSathi Java Backend Production Dockerfile
# Optimized for Render Web Service Deployment
# ==========================================

# Stage 1: Build the Java Fat-JAR
FROM maven:3.9.6-eclipse-temurin-17 AS build
WORKDIR /app

# Copy pom.xml and dependency definitions
COPY pom.xml .

# Download dependencies offline cache
RUN mvn dependency:go-offline -B || true

# Copy source code and data rules
COPY src ./src
COPY data ./data

# Build the standalone Fat-JAR with all dependencies
RUN mvn clean package -DskipTests

# Stage 2: Lightweight JRE 17 Runtime
FROM eclipse-temurin:17-jre
WORKDIR /app

# Copy artifact and required data files from build stage
COPY --from=build /app/target/schemesathi-1.0.0-jar-with-dependencies.jar ./app.jar
COPY --from=build /app/data ./data

# Set default port (Render dynamically sets $PORT at runtime)
ENV PORT=8080
EXPOSE 8080

# Launch server using dynamic PORT environment variable
CMD ["sh", "-c", "java -jar app.jar --server --port ${PORT:-8080}"]
