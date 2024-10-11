import random
from flask import Flask, request, render_template_string
import TaskKnutMax
from datetime import datetime


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
        <div class="flex">
            <!-- Sidebar with all routes -->
            <div class="w-1/3 bg-white p-4 rounded-xl shadow-md">
                <h3 class="text-lg font-semibold mb-4">Available Routes</h3>
                {% if all_routes %}
                <ul class="space-y-2">
                    {% for route in all_routes %}
                    <li class="p-2 border border-gray-200 rounded">
                        <strong>Route:</strong> {{ route['road'] }}<br>
                        <strong>Departure:</strong> {{ route['depature'] }}<br>
                        <strong>Arrival:</strong> {{ route['arrival'] }}<br>
                        <strong>Travel Time:</strong> {{ route['travel_time'] }}
                    </li>
                    {% endfor %}
                </ul>
                {% else %}
                <p>No matching routes found.</p>
                {% endif %}
            </div>

            <!-- Main content area -->
            <div class="w-2/3 ml-4">
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
    departure_m = request.args.get('mins') or '00'

    # Get best route and all matching routes
    result = TaskKnutMax.get_the_best_route_as_a_text_informatic(departure_h, departure_m)

    # Check if result is a dict and has matching routes
    if isinstance(result, dict):
        all_routes = sorted(result['matching_routes'], key=lambda x: (
                datetime.strptime(x['arrival'], "%H:%M") - datetime.strptime(x['depature'], "%H:%M")).total_seconds())

        # Add formatted travel time for each route
        for route in all_routes:
            dep_time = datetime.strptime(route['depature'], "%H:%M")
            arr_time = datetime.strptime(route['arrival'], "%H:%M")
            travel_time = arr_time - dep_time
            hours, remainder = divmod(travel_time.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            route['travel_time'] = f"{hours}h {minutes}m"
        TaskKnutMax.plot_routes(result['matching_routes'], result)
        return render_template_string(TEMPLATE, route_info=result, all_routes=all_routes)

    return render_template_string(TEMPLATE, route_info=None, all_routes=[])


if __name__ == '__main__':
    app.run(debug=True)
