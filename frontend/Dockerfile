# Use Bun official image
FROM oven/bun:1

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json bun.lockb* ./

# Install dependencies
RUN bun install

# Copy rest of the app
COPY . .

# Expose port (same as before)
EXPOSE 3000

# Start dev server
CMD ["bun", "run", "dev"]