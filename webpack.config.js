var path = require('path');

var OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');

var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
    entry: './static/js/index.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'static/js')
    },
    module: {
        loaders: [
            {
                test: /\.scss$/, loader: ExtractTextPlugin.extract({
                    fallback: 'style-loader',
                    use: ['css-loader', 'sass-loader']
                })
            },
            {
                test: /\.js$/, exclude: /node_modules/, loader: "babel-loader"
            }
        ]
    },
    plugins: [
        new ExtractTextPlugin("../css/styles.css"),
        new OptimizeCssAssetsPlugin({
            assetNameRegExp: /\.optimize\.css$/g,
            cssProcessor: require('cssnano'),
            cssProcessorOptions: { discardComments: {removeAll: true}},
            canPrint: true
        })
    ]
};
