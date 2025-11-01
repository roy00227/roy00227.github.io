module.exports = function(eleventyConfig) {
    
    // --- �ȑO�̐ݒ�istyle.css��js�t�H���_�j ---

    // 画像ファイル群
    eleventyConfig.addPassthroughCopy("android-chrome-192x192.png");
    eleventyConfig.addPassthroughCopy("android-chrome-512x512.png");
    eleventyConfig.addPassthroughCopy("apple-touch-icon.png");
    eleventyConfig.addPassthroughCopy("favicon.ico");
    eleventyConfig.addPassthroughCopy("favicon-16x16.png");
    eleventyConfig.addPassthroughCopy("favicon-32x32.png");
    eleventyConfig.addPassthroughCopy("favicon-64x64.png");

    // 設定ファイル群
    eleventyConfig.addPassthroughCopy("manifest.json");
    eleventyConfig.addPassthroughCopy("robots.txt");
    eleventyConfig.addPassthroughCopy("sitemap.xml");

    // CSSファイル
    eleventyConfig.addPassthroughCopy("style.css");
    eleventyConfig.addPassthroughCopy("js");
    
    // ----------------------------------------
    // �� image�t�H���_�̒ǉ� ��
    // ----------------------------------------
    eleventyConfig.addPassthroughCopy("image"); // �� ���̍s��ǉ�

    // ----------------------------------------
    // �� �L�����̉摜���R�s�[����ݒ�i�d�v�j��
    // ----------------------------------------

    // 特定のフォルダ全体をコピーしたい場合は、フォルダ名を指定します
    // 例: document/loading-screen-with-load-percentage/image フォルダ全体をコピー
    eleventyConfig.addPassthroughCopy("document/**/image");

    // 特定のフォルダ全体をコピーしたい場合は、フォルダ名を指定します
    // 例: document/loading-screen-with-load-percentage/image フォルダ全体をコピー
    eleventyConfig.addPassthroughCopy("memo/**/image");

    // 特定のフォルダ全体をコピーしたい場合は、フォルダ名を指定します
    // 例: document/loading-screen-with-load-percentage/image フォルダ全体をコピー
    eleventyConfig.addPassthroughCopy("portfolio/**/image");
    
    
return {
    // ★ HTMLファイルをテンプレートとして処理する設定を追加/確認 ★
    htmlTemplateEngine: "liquid",
    markdownTemplateEngine: "liquid",
    dataTemplateEngine: "liquid",
    
    // 処理対象ファイルに "html" を含める
    templateFormats: ["md", "html", "liquid", "njk", "css", "js"], 
    
    dir: {
        input: ".",
        output: "_site"
    }
};
};