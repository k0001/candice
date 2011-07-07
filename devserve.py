import os
os.environ['CANDICE_SETTINGS'] = 'settings_development.py'

from candice import app
app.run(debug=True, host='0.0.0.0', port=5000)
