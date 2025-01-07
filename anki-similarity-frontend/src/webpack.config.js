module.exports = {
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules\/(?!(your-package-name)\/).*/, // Replace `your-package-name` with `@mui`
        use: {
          loader: 'babel-loader',
        },
      },
    ],
  },
};