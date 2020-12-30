const HtmlWebPackPlugin = require("html-webpack-plugin");
const path = require("path");
module.exports = {
  context: __dirname,
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "main.js",
  },
  module: {
    rules: [
      {
        test: /\.html$/i,
        loader: "html-loader",
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
  devServer: {
    port: 4000,
    contentBase: __dirname + "/dist",
    watchContentBase: true,
    inline: false,
    clientLogLevel: "info",
  },

  plugins: [],
};

//new HtmlWebPackPlugin()
