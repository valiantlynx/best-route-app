import random
from flask import Flask, request, render_template_string
import TaskKnutMax

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Knut Knut Transport AS</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 text-gray-900">
    <div class="container mx-auto p-8">
        <div class="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl">
            <div class="p-6">
                <h3 class="text-2xl font-semibold text-center mb-6">Knut Knut Transport AS</h3>
                <form action="/get_best_route" method="get" class="space-y-4">
                    <div>
                        <label for="hour" class="block text-sm font-medium text-gray-700">Hour:</label>
                        <select name="hour" id="hour" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
                            {% for i in range(7, 17) %}
                                <option value="{{ '%02d'|format(i) }}">{{ '%02d'|format(i) }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div>
                        <label for="mins" class="block text-sm font-medium text-gray-700">Minutes:</label>
                        <input type="text" name="mins" id="mins" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" placeholder="00" size="2"/>
                    </div>

                    <div class="flex justify-center">
                        <button type="submit" class="px-4 py-2 bg-indigo-600 text-white font-semibold rounded-md hover:bg-indigo-700 shadow-md">Get Best Route</button>
                    </div>
                </form>

                {% if route_info %}
                <div class="mt-6">
                    <h4 class="text-xl font-semibold">Best Route Information:</h4>
                    <ul class="mt-3 space-y-2">
                        <li><strong>Departure:</strong> {{ route_info['departure'] }}</li>
                        <li><strong>Arrival:</strong> {{ route_info['arrival'] }}</li>
                        <li><strong>Best Time:</strong> {{ route_info['best_time'] }}</li>
                        <li><strong>Route:</strong> {{ route_info['route'] }}</li>
                    </ul>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>
"""


@app.route('/')
def get_departure_time():
    return render_template_string(TEMPLATE)


@app.route("/get_best_route")
def get_route():
    departure_h = request.args.get('hour')
    departure_m = request.args.get('mins') or 00

    # Call your actual function here
    route_info = TaskKnutMax.get_the_best_route_as_a_text_informatic(departure_h, departure_m)

    # If TaskKnutMax isn't available or for testing purposes, you can use a mock route_info
    # route_info = {
    #     "departure": f"{departure_h}:{departure_m}",
    #     "arrival": "11:12",
    #     "best_time": "1h 3m",
    #     "route": "B->C->D"
    # }

    return render_template_string(TEMPLATE, route_info=route_info)


if __name__ == '__main__':
    app.run(debug=True)
