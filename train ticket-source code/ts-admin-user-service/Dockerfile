# ==============================================================================
# Multi-Stage Build: Footprint & Memory Optimized
# ==============================================================================

# Stage 1: Build Stage (Lightweight Alpine Maven Builder)
FROM maven:3.9-eclipse-temurin-11-alpine AS builder
WORKDIR /build

# Copy root pom and dependencies
COPY . .
RUN mvn -q -pl ts-admin-user-service -am clean package -DskipTests

# Stage 2: Ultra-low footprint Alpine JRE Runtime
FROM eclipse-temurin:11-jre-alpine AS runtime
WORKDIR /app

# Create non-root user for security and resource optimization
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy solely the packaged artifact
COPY --from=builder --chown=appuser:appgroup /build/ts-admin-user-service/target/*.jar app.jar

USER appuser

# Expose Service Port
EXPOSE 16115

# Container Memory Optimization JVM parameters
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -XX:+ExitOnOutOfMemoryError -XX:+TieredCompilation -XX:TieredStopAtLevel=1 -Djava.security.egd=file:/dev/./urandom"

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
