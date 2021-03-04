module.exports = {
  devServer: {
    // assetsSubDirectory: 'static',
    // assetsPublicPath: '/',
    proxy: {
      "/qwe": {
        target: "http://127.0.0.1:8087/file",
        changeOrigin: true,
        pathRewrite: {
          "^/qwe": ""
        }
      },
      "/voi": {
        target: "http://127.0.0.1:8087/getvoi",
        changeOrigin: true,
        pathRewrite: {
          "^/voi": ""
        }
      }
    }
  }
};
