

# 文件下载
@app.route('/download/<path:filename>')
def send_html(filename):
    logger.debug("download file, path is %s" % filename)
    return send_from_directory(app.config['UPLOAD_PATH'], filename, as_attachment=True)