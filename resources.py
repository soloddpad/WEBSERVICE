from flask import request, jsonify, make_response
from flask_restful import Resource
from models import db, Infrastructure


class InfrastructureResource(Resource):
    def get(self, id=None):
        if id:
            infra = Infrastructure.query.get_or_404(
                id)
            response_data = {"id": infra.id,
                             "name": infra.name, "location": infra.location}
        else:
            infra_list = Infrastructure.query.all()
            response_data = [{"id": infra.id, "name": infra.name,
                              "location": infra.location} for infra in infra_list]

        response = make_response(jsonify(response_data))

        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response

    def post(self):
        data = request.get_json()
        name = data['name']
        location = data['location']

        new_infra = Infrastructure(
            name=name,
            location=location
        )

        db.session.add(new_infra)
        db.session.commit()
        response_data = {"message": "Успешно добавлено",
                         "id": new_infra.id}
        response = make_response(jsonify(response_data), 201)

        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response


class InfrastructureSearchResource(Resource):
    def get(self):
        name = request.args.get('name')
        location = request.args.get('location')

        query = Infrastructure.query

        if name:
            query = query.filter(Infrastructure.name.like(f'%{name}%'))
        if location:
            query = query.filter(Infrastructure.location.like(f'%{location}%'))

        infra_list = query.all()
        response_data = [{"id": infra.id, "name": infra.name,
                          "location": infra.location} for infra in infra_list]
        response = make_response(jsonify(response_data))

        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
