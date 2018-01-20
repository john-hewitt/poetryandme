const webpack = require('webpack');
const config = {
    entry:  __dirname + '/../static/src/app.jsx',
    output: {
        path: __dirname + '/../static/dist',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },
    module: {
        rules: [
            {
              test: /\.jsx?/,
              exclude: /node_modules/,
              use: 'babel-loader',
              //loader: 'babel',
              /*query: {
                presets: ['react']
              }*/
            }
        ]
        // loaders: [
        //     {
        //         test: /\.html$/,
        //         loader: 'file-loader?name=[name].[ext]',
        //     },
        //     {
        //         test: /\.jsx?$/,
        //         exclude: /node_modules/,
        //         loader: 'babel-loader',
        //         query: {
        //           presets: ['es2015', 'react']
        //         }
        //     },
        // ]
    }
};
module.exports = config;