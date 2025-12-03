FROM liquibase/liquibase:latest

# Create lib directory
RUN mkdir -p /liquibase/lib

# Copy Snowflake JDBC driver
COPY libs/snowflake-jdbc-3.16.1.jar /liquibase/lib/

# Copy CA certificates
COPY libs/cacert.pem /tmp/cacert.pem

# Switch to root user to import certificate
USER root

RUN keytool -importcert -noprompt -trustcacerts \
    -alias customCA \
    -file /tmp/cacert.pem \
    -cacerts \
    -storepass changeit

# Switch back to liquibase user
USER liquibase