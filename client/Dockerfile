# Step 1: Use Node.js to build the React app
#FROM node:18 AS build <---- when not in debug
FROM node:18 

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
#FROM nginx:alpine <---- remove cmment when not in debug

# Copy the built React app from the previous step to Nginx's web root
#COPY --from=build /app/build /usr/share/nginx/html <---- remove cmment when not in debug

# Expose port 80 to the host
EXPOSE 3000
CMD ["npm", "start"]

#EXPOSE 80
#CMD ["nginx", "-g", "daemon off;"]
