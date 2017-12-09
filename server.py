#!/user/bin/python
import re
import numpy as np
from flask import Flask
import argparse
from flask import jsonify
from flask import request
from flask import abort
from flask import make_response
from pymongo import MongoClient
from bson.objectid import ObjectId


server = Flask(__name__)

client = MongoClient()
db = client.songs


@server.route('/songs', methods=['GET'])
def get_songs():
	cursor = db.songs.find({}, {'_id':0})
	res = [song for song in cursor]
	return make_response(jsonify({'result':res}), 200)


@server.route('/songs/search', methods=['GET'])
def get_songs_search():
	data = request.args
	if not data or not 'message' in data:
		abort(400)
	message = data.get('message')
	cursor = db.songs.find({'$or':[
		{'title': re.compile(message, re.IGNORECASE)},
		{'artist': re.compile(message, re.IGNORECASE)}]}
		, {'_id':0})

	res = [song for song in cursor]
	return make_response(jsonify({'result':res}), 200)


@server.route('/songs/avg/difficulty', methods=['GET'])
def get_avg_difficulty():
	data = request.args
	if not data or not 'level' in data:
		cursor = db.songs.find({}, {'difficulty':1, '_id':0})
	else:
		level = int(data.get('level'))
		cursor = db.songs.find({'level':level}, {'difficulty':1, '_id':0})

	res = [song['difficulty'] for song in cursor]
	avg = np.average(res)	

	return make_response(jsonify({'result':avg}), 200)

@server.route('/songs/rating', methods=['POST'])
def add_rating():
	data = request.form
	if not data or not 'song_id' in data or not  'rating' in data:
		abort(400)

	song_id = data.get('song_id')
	rating = int(data.get('rating'))

	if not (1<= rating <=5):
		abort(400)

	db.songs.update({'title':song_id}, {'$push' : {"rating":rating}})

	cursor = db.songs.find({'title':song_id}, {'_id':0})
	res = [song for song in cursor]

	return make_response(jsonify({'result':res}), 200)	


@server.route('/songs/avg/rating/<song_id>', methods=['GET'])
def get_rating(song_id):
	if not song_id:
		abort(400)
	cursor = db.songs.find({'title':song_id}, {'rating':1, '_id':0})
	res = dict()
	for song in cursor:
		res['highest'] = max(song['rating'])
		res['lowest'] = min(song['rating'])
		res['average'] = np.average(song['rating'])
	return make_response(jsonify({'result':res}), 200)


@server.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': "The request could not be understood by the server due to malformed syntax. "
    	"The client SHOULD NOT repeat the request without modifications."}), 400)


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Yousician Server')
	parser.add_argument('-P', action="store", dest="server_port",
		default=5000, type=int, help="Server Listening Port")
	
	args = parser.parse_args()

	port = args.server_port

	server.run(debug=True, port=port)