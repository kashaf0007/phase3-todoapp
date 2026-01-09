/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    unoptimized: true,
  },
  experimental: {
    turbo: {
      enabled: false
    }
  },
};

module.exports = nextConfig;