# Official MongoDB image from Docker Hub
FROM mongo:latest

# Set environment variables for MongoDB
ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD=securepassword

# Expose MongoDB port
EXPOSE 27017

# Create a directory for MongoDB data
RUN mkdir -p /data/db

# Set the ownership of the data directory to the MongoDB user
RUN chown -R mongodb:mongodb /data/db

# Define a volume to persist data
VOLUME /data/db

# Copy the MongoDB configuration file
COPY mongod.conf /etc/mongod.conf

# Run MongoDB with the specified configuration file
CMD ["mongod", "--config", "/etc/mongod.conf"]
