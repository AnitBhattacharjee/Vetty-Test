from flask import Flask, render_template, request
import chardet

app = Flask(__name__)

@app.route('/file_content/', defaults={'filename': 'file1.txt'}, methods=['GET'])
@app.route('/file_content/<filename>', methods=['GET'])
def file_content(filename):
    start_line = request.args.get('start_line', None)
    end_line = request.args.get('end_line', None)
    
    try:
        with open(f'files/{filename}', 'rb') as file:
            data = file.read()
            encoding_info = chardet.detect(data)
            encoding = encoding_info['encoding']
        
        
        if encoding is None:
            raise Exception("Failed to detect encoding.")
        
    
        with open(f'files/{filename}', 'r', encoding=encoding) as file:
            lines = file.readlines()
            
            if start_line is not None and end_line is not None:
                start_line = int(start_line)
                end_line = int(end_line)
                content = ''.join(lines[start_line-1:end_line])
            else:
                content = ''.join(lines)
        
        return render_template('file_content.html', content=content)
    except FileNotFoundError:
        return render_template('error.html', message='File not found.')
    except Exception as e:
        return render_template('error.html', message=f'An error occurred: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
