# Use an official Node.js image
FROM node:20-slim

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to leverage cache
COPY package*.json ./

# Install dependencies
RUN npm install && npm audit fix --force

# Copy the rest of the frontend code
COPY . .

# Expose the Vite port
EXPOSE 5173

# Command to run the Vite dev server, accessible from outside the container
CMD ["npm", "run", "dev", "--", "--host"]