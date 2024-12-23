from flask import Flask, render_template, request, make_response, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/profile')
def profile_settings():
    
    if 'username' not in session:
        return redirect('login')
    
    # Präferenzen aus Datenbank laden
    username = session['username']
    user_preferences = users[username]['preferences']

    # Standard-Präferenzen aus Cookies
    # audio_enabled = request.cookies.get('audio_enabled', 'True') == 'True'
    # subtitles_enabled = request.cookies.get('subtitles_enabled', 'True') == 'True'
    # speed = float(request.cookies.get('speed', '1.0'))
    
    return render_template('profile.html', preferences=user_preferences)


@app.route('/set_preferences', methods=['POST'])
def set_preferences():
    # neue Präferenzen lesen
    audio_enabled = request.form.get('audio_enabled') == 'true'
    subtitles_enabled = request.form.get('subtitles_enabled') == 'true'
    speed = request.form.get('speed', '1.0')
    pikto_enabled = request.form.get('pikto_enabled') == 'true'
    subtitle_style = request.form.get('subtitle_style', 'white-outline')
    subtitle_size = request.form.get('subtitle_size', 'medium')
    music_enabled = request.form.get('music_enabled') == 'true'

    # Präferenzen in "Datenbank" speichern
    if 'username' in session:
        username = session['username']
        users[username]['preferences'] = {
            'audio': audio_enabled,
            'subtitles': subtitles_enabled,
            'speed': float(speed),
            'pikto': pikto_enabled,
            'subtitle_style': subtitle_style,
            'subtitle_size': subtitle_size,
            'music': music_enabled
        }
    # Präferenzen in Cookies speichern    
    else:     
        resp = make_response(redirect(request.referrer))
        resp.set_cookie('audio_enabled', str(audio_enabled))
        resp.set_cookie('subtitles_enabled', str(subtitles_enabled))
        resp.set_cookie('speed', speed)
        resp.set_cookie('pikto_enabled', str(pikto_enabled))
        resp.set_cookie('subtitle_style', subtitle_style)
        resp.set_cookie('subtitle_size', subtitle_size)
        resp.set_cookie('music_enabled', str(music_enabled))
        return resp

    return redirect(request.referrer)


@app.route('/gallery')
def video_gallery():
    # Videos im static-Folder
    videos = ['video1', 'video2', 'video3']
    return render_template('gallery.html', videos=videos)

@app.route('/video/<video_name>')
def video(video_name):

    #Präferenzen von Account
    if 'username' in session:
        username = session['username']
        preferences = users[username]['preferences']

    #Präferenzen aus Cookies mit Standardwerten
    else:
        preferences = {
            'audio': request.cookies.get('audio_enabled', 'True') == 'True',
            'subtitles': request.cookies.get('subtitles_enabled', 'True') == 'True',
            'speed': float(request.cookies.get('speed', '1.0')),
            'pikto': request.cookies.get('pikto_enabled', 'True') == 'True',
            'subtitle_style': request.cookies.get('subtitle_style', 'white-outline'),
            'subtitle_size': request.cookies.get('subtitle_size', 'medium'),
            'music': request.cookies.get('music_enabled', 'True') == 'True'
        }    

    return render_template(
        'video.html',
        video_src=f"{video_name}.mp4",
        subtitle_src = f"{video_name}.vtt",
        audio=preferences['audio'],
        subtitles=preferences['subtitles'],
        speed=preferences['speed'],
        pikto=preferences['pikto'],
        subtitle_style=preferences['subtitle_style'],
        subtitle_size=preferences['subtitle_size'],
        music=preferences['music']
    )
    


#Login

#Simulierte Datenbank
users = {
    'user1': {
        'password': 'pass1', 
        'preferences': {
            'audio': True, 
            'subtitles': True, 
            'speed': 1.0,
            'pikto': True,
            'subtitle_style': 'semi-transparent', # white-outline, yellow-outline, semi-transparent
            'subtitle_size': 'medium',
            'music': False
        }
    },

    'user2': {
        'password': 'pass2',
        'preferences': {
            'audio': True, 
            'subtitles': True, 
            'speed': 1.0,
            'pikto': True,
            'subtitle_style':'semi-transparent',
            'subtitle_size': 'medium',
            'music': False
        }
    }
}   


@app.route('/login', methods=['GET', 'POST'])
def login():
    error_msg = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        #Benutzerüberprüfung
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error_msg = 'Username or password is wrong. Please, try again!'

    return render_template('login.html', error_msg=error_msg)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)