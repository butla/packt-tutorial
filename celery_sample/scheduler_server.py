import json
import falcon
import tasks


class SchedulerResource:
    def on_post(self, req, resp):
        req_json = json.loads(req.stream.read())
        the_number = req_json['number']

        tasks.print_factorial_digits.delay(the_number)

        resp.status = falcon.HTTP_ACCEPTED
        # we would need to implement this
        resp.content_location = 'https://some_fake/task_status_indicator'


application = falcon.API()
application.add_route('/', SchedulerResource())
