import type { NextConfig } from "next";
import path from "path";

const root = path.resolve(__dirname, "..");

const nextConfig: NextConfig = {
  outputFileTracingRoot: root,
  turbopack: {
    root,
  },
};

export default nextConfig;
