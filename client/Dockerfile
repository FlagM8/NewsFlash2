# Step 1: Use Node.js to build the React app
FROM node:18 AS build

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# Step 2: Use Nginx to serve the built application
FROM nginx:alpine

# Copy the built React app from the previous step to Nginx's web root
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 to the host
#EXPOSE 80
EXPOSE 3000

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
