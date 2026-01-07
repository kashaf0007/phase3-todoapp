/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  serverExternalPackages: ['@tanstack/react-query'],
  images: {
    unoptimized: true,
  },
  // Configure Turbopack explicitly to avoid conflicts
  turbopack: {},
  webpack: (config, { isServer }) => {
    // Ensure that the 'src' alias is properly resolved by webpack
    config.resolve.alias = {
      ...config.resolve.alias,
      src: __dirname + '/src',
    };
    return config;
  },
};

module.exports = nextConfig;