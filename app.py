from flask import Flask, request, render_template, send_from_directory, redirect
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/home')
def home():
    # Diese Route lädt die Homepage
    return render_template('home.html')

@app.route('/')
def index():
    return render_template('index.html')  # Dein HTML-Formular

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return "Keine Datei hochgeladen", 400
    file = request.files['image']

    if file.filename == '':
        return "Kein Dateiname angegeben", 400
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    title = request.form.get('title')
    description = request.form.get('description')

    # Speichern der Metadaten in einer separaten .txt-Datei
    metadata_path = os.path.splitext(file_path)[0] + '.txt'
    with open(metadata_path, 'w') as metadata_file:
        metadata_file.write(f"{title}\n{description}")

    # Weiterleitung zur Upload-Seite nach erfolgreichem Hochladen
    return redirect('/')  # Hier wird der Benutzer zur Upload-Seite zurückgeführt



@app.route('/gallery')
def gallery():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    image_data = {}

    for file in files:
        if file.endswith(('.jpg', '.jpeg', '.png')):  # Nur Bilddateien einbeziehen
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            metadata_path = file_path.rsplit('.', 1)[0] + '.txt'  # Pfad zur metadata.txt

            print(f"Überprüfe Metadaten für {file}: {metadata_path}")

            # Prüfen, ob die metadata.txt existiert
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = f.read().splitlines()
                    title = metadata[0]  # Titel
                    description = metadata[1]  # Beschreibung
                    print(f"Metadaten geladen für {file}: {title}, {description}")
            else:
                title = "Kein Titel"
                description = "Keine Beschreibung"
                print(f"Keine Metadaten gefunden für {file}")

            image_data[file] = {
                'title': title,
                'description': description
            }

    return render_template('gallery.html', image_data=image_data)



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
