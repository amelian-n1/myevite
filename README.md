# Myevite

A group project for Coding Dojo by @amelian-n1 and @fostercoryj.

# The Problem

<img align="right" src="/images/facebook_data.png" width="350" />

Throughout our early adult lives, we have used Facebook events as an easy way to invite friends to personal events like house warmings and birthday parties. We love that the app keeps track of RSVPs, so we can avoid making yet another spreadsheet.

However, over the years we noticed that more and more of our peers and no longer using the platform. While most of our friends still have Facebook profiles, they are not engaging with the platform as often as they used to.

Data supports this - research has shown (see graph) that young people are increasingly using YouTube, Snapchat, and Instagram rather than Facebook.

If our desired attendees are not checking their Facebooks, how can we invite them to an event and track their responses?

# The Solution


<img align="right" src="/images/event_form.png" width="350" />

We set out to build an easy to use RSVP form creator for users to invite friends to their events and keep track of RSVPs. Rather than sending an invitation to a hand picked list of Facebook friends, users would distribute the evites themselves over email or text - whatever way they could most easily reach their desired guests.

Users would first register their email address and create a password that would be encrypted and stored in the database. This would allow for all of their events to be stored in one secure location.

After registering, users would login and be directed to the Create an event form. Following the Facebook model, users would enter all necessary details of their upcoming event including time, date, location and description.

After clicking submit, the user would be directed to the Dashboard. As the central home of the app, the Dashboard includes all of their events, evites, and quick snapshots of the RSVPs.

Clicking on Event details would show all of the details submitted in the event form and provide a list of all of the RSVPed guests, including their names and email addresses.

Clicking on My evite would open the event invitation with all of their specified details and RSVP form. To make it easy for attendees to find the event location, we added the Google Map API which shows a map of the physical location.

<br>

<p align="middle">
  <img src="/images/dashboard.png" width="600" />
  <img src="/images/event_details.png" width="600" />
  <img src="/images/RSVP.png" width="600" />
</p>

# Built With
Python, Django, HTML, Materialize

# Installation
Activate your Django virtual environment.

Navigate to the downloaded folder in your terminal. Run the following command.

‘’’ $ python manage.py runserver ‘’’

Go to localhost:8000 in your web browser.
