module.exports = {
    // Entry point for webpack. Add new components here
    entry: {
        survey: './cocoon/frontend/src/survey',
        userAuth: './cocoon/frontend/src/userAuth',
        scheduler: './cocoon/frontend/src/scheduler',
        signature: './cocoon/frontend/src/signature',
        surveyResults: './cocoon/frontend/src/surveyResults'
    },
    // Output name and directory for components
    output: {
        filename: '[name].bundle.js',
        path: __dirname + '/cocoon/frontend/static/frontend/js'
    },
    module: {
        rules: [
            // Transpiles js code down to ES5
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            },
            // Adds ability to import css files into react components
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            // Adds ability to import images into components
            {
                test: /\.(gif|svg|jpg|png)$/,
                loader: "url-loader?limit=1000000"
            }
        ]
    }
};