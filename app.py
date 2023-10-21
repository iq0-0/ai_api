from flask import Flask, jsonify, request

from read_face import get_attendance

app = Flask(__name__) 
  

@app.route('/', methods = ['GET', 'POST']) 
def home(): 
    data = "Hello World!"
    return jsonify({'data': data}) 
      

@app.route('/ai', methods = ['POST']) 
async def take_image():
    data = request.get_json()
    if "Lecture" not in data and "Students" not in data:
        return jsonify({"Error":"Failed To read Lecture or Students"}) 
    if "Lecture" not in data:
        return jsonify({"Error":"Failed To read Lecture"}) 
    if "Students" not in data:
        return jsonify({"Error":"Failed To read Students"}) 

    data = await get_attendance(students=data["Students"], lecture=data["Lecture"])
    return jsonify(data) 

  
# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True) 