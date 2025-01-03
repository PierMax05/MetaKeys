module.exports = {
  presets: [
    ['@babel/preset-env', { targets: "defaults" }]
  ],
  plugins: [
    ['@babel/plugin-proposal-decorators', { legacy: true }],
    ['@babel/plugin-proposal-class-properties', { loose: true }]
  ]
};