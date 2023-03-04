### GET EVENTS

calendarEvents = service.events().list(calendarId=calendarIds[0]).execute()
print(calendarEvents["items"][0])


### MAKE AN EVENT

testEvent = {
	"summary": "Random Test Event",
	"location": "10 Downing Street, London",
	"description": "test event for a level project",
	"start": {
		"dateTime": "2022-09-30T16:35:00",
		"timeZone": "Europe/London"
	},
	"end": {
		"dateTime": "2022-09-30T17:00:00",
		"timeZone": "Europe/London"
	},
	# "recurrence": []
	"attendees": [],
	"reminders": {
		"useDefault": False,
		"overrides": [
			{
				"method": "email",
				"minutes": 15
			}
		]

	}
}
service.events().insert(calendarId=calendarIds[0], body=testEvent).execute()



