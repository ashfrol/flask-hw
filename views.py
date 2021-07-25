from flask import request, jsonify
from flask.views import MethodView

from app import app
from models import Ad
from schema import AD_CREATE
from validator import validate


class AdView(MethodView):
    def get(self, ad_id=None):
        ad = Ad.by_id(ad_id)
        return jsonify(ad.to_dict())

    @validate('json', AD_CREATE)
    def post(self):
        ad = Ad(**request.json)
        Ad.add(ad)
        return jsonify(ad.to_dict())

    def delete(self, ad_id):
        ad = Ad.by_id(ad_id)
        ad.del_obj()
        return {
            'id': ad_id,
            'message': 'Объявление успешно удалено'
        }


@app.route('/health/', methods=['GET', ])
def health():
    if request.method == 'GET':
        return jsonify({'status': 'OK'})

    return {'status': 'OK'}


ad_api = AdView.as_view('ads_api')
app.add_url_rule('/ad/', view_func=ad_api, methods=['POST', ])
app.add_url_rule('/ad/<int:ad_id>', view_func=ad_api, methods=['GET', 'DELETE', ])
