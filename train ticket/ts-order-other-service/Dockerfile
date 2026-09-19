# Build stage: build from the repository root (compose sets context: .)
# so the parent POM and the ts-common dependency are available to Maven.
# .dockerignore keeps the context lean.
FROM maven:3.8.1-jdk-11-slim AS build
WORKDIR /build
COPY . .
RUN mvn -q -pl ts-order-other-service -am package -DskipTests

# Runtime stage
FROM eclipse-temurin:11-jre
WORKDIR /app
COPY --from=build /build/ts-order-other-service/target/*.jar app.jar
EXPOSE 12032
ENTRYPOINT ["java", "-Xmx512m", "-jar", "app.jar"]
