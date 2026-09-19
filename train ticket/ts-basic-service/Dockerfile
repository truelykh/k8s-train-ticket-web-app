# Build stage: build from the repository root (compose sets context: .)
# so the parent POM and the ts-common dependency are available to Maven.
# .dockerignore keeps the context lean.
FROM maven:3.8.1-jdk-11-slim AS build
WORKDIR /build
COPY . .
RUN mvn -q -pl ts-basic-service -am package -DskipTests

# Runtime stage
FROM eclipse-temurin:11-jre
WORKDIR /app
COPY --from=build /build/ts-basic-service/target/*.jar app.jar
EXPOSE 15680
ENTRYPOINT ["java", "-Xmx512m", "-jar", "app.jar"]
