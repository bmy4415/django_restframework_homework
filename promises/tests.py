import unittest
from datetime import datetime, timedelta

import pytz
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from promises import models


def iso8601(dt):
    return dt.isoformat()


class PromisesUtilMixins(unittest.TestCase):
    timezone = pytz.utc
    dtformats = [
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%dT%H:%M:%SZ'
    ]

    def create_user(self, username):
        user = User(username=username)
        user.save()
        setattr(self, username, user)
        return user

    def create_promises_between_users(self, users):
        time = datetime(2018, 4, 1).astimezone(self.timezone)
        for inviter in users:
            for invitee in users:
                if inviter == invitee:
                    continue
                promise = models.Promise(
                    sinceWhen=time,
                    tilWhen=time + timedelta(hours=1),
                    user1=inviter,
                    user2=invitee)
                promise.save()
                setattr(self, f'promise_{inviter.username}_{invitee.username}', promise)
                time = time + timedelta(hours=1)

    @classmethod
    def _to_datetime(cls, dt):
        if isinstance(dt, datetime):
            return dt
        if isinstance(dt, str):
            for fmt in cls.dtformats:
                try:
                    return datetime.strptime(dt, fmt).astimezone(cls.timezone)
                except ValueError:
                    continue
            raise ValueError('Invalid format: ' + dt)
        raise TypeError('Invalid type: ' + str(type(dt)))

    def assertDateTimeEqual(self, dt1, dt2):
        dt1 = self._to_datetime(dt1)
        dt2 = self._to_datetime(dt2)
        self.assertEqual(dt1, dt2)

    def assertDateTimeNotEqual(self, dt1, dt2):
        dt1 = self._to_datetime(dt1)
        dt2 = self._to_datetime(dt2)
        self.assertNotEqual(dt1, dt2)

    def assertFieldsEqual(self, data, **fields):
        for field, value in fields.items():
            if isinstance(value, dict):
                self.assertEqual(data[field], **value)
            elif isinstance(value, list):
                self.assertListEqual(data[field], value)
            elif isinstance(value, datetime):
                self.assertDateTimeEqual(data[field], value)
            else:
                self.assertEqual(data[field], value)

    def assertFieldsNotEqual(self, data, **fields):
        for field, value in fields.items():
            if isinstance(value, dict):
                self.assertFieldsNotEqual(data[field], **value)
            elif isinstance(value, datetime):
                self.assertDateTimeNotEqual(data[field], value)
            else:
                self.assertNotEqual(data[field], value)


class TestPromises(TestCase, PromisesUtilMixins):
    timezone = pytz.utc

    def setUp(self):
        messi = self.create_user('messi')
        ronaldo = self.create_user('ronaldo')
        neymar = self.create_user('neymar')
        self.create_promises_between_users([messi, ronaldo, neymar])
        self.client = APIClient()

    def test_list_promises(self):
        # when
        resp = self.client.get('/promises/')

        # then
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 6)

    def test_get_promise(self):
        # setup
        self.client.force_authenticate(user=self.ronaldo)

        # when
        resp = self.client.get(f'/promises/{self.promise_ronaldo_messi.id}/')

        # then
        self.assertEqual(resp.status_code, 200)
        self.assertFieldsEqual(resp.data,
                               user1=self.ronaldo.id,
                               user2=self.messi.id)

    def test_get_promise_without_authentication(self):
        # when
        resp = self.client.get(f'/promises/{self.promise_ronaldo_messi.id}/')

        # then
        self.assertEqual(resp.status_code, 403)

    def test_get_promise_of_others(self):
        # setup
        self.client.force_authenticate(user=self.ronaldo)

        # when
        resp = self.client.get(f'/promises/{self.promise_messi_neymar.id}/')

        # then
        self.assertEqual(resp.status_code, 403)

    def test_get_nonexisting_promise(self):
        # setup
        self.client.force_authenticate(user=self.ronaldo)

        # when
        resp = self.client.get(f'/promises/9999/')

        # then
        self.assertEqual(resp.status_code, 404)

    def test_create_promise(self):
        # setup
        promise_since = self.timezone.localize(datetime.now())
        promise_until = promise_since + timedelta(hours=1)
        self.client.force_authenticate(user=self.ronaldo)

        # when
        resp = self.client.post('/promises/', data={
            'sinceWhen': iso8601(promise_since),
            'tilWhen': iso8601(promise_until),
            'user2': self.messi.id
        })

        # then
        self.assertEqual(resp.status_code, 201)
        self.assertFieldsEqual(resp.data,
                               user1=self.ronaldo.id,
                               user2=self.messi.id,
                               sinceWhen=promise_since,
                               tilWhen=promise_until)

    def test_create_promise_invalid_timespan(self):
        # setup
        promise_since = self.timezone.localize(datetime.now())
        promise_until = promise_since - timedelta(hours=1)
        self.client.force_authenticate(user=self.ronaldo)

        # when
        resp = self.client.post('/promises/', data={
            'sinceWhen': iso8601(promise_since),
            'tilWhen': iso8601(promise_until),
            'user2': self.messi.id
        })

        # then
        self.assertEqual(resp.status_code, 400)

    def test_create_promise_with_myself(self):
        # setup
        promise_since = self.timezone.localize(datetime.now())
        promise_until = promise_since + timedelta(hours=1)
        self.client.force_authenticate(user=self.ronaldo)

        # when
        resp = self.client.post('/promises/', data={
            'sinceWhen': iso8601(promise_since),
            'tilWhen': iso8601(promise_until),
            'user2': self.ronaldo.id
        })

        # then
        self.assertEqual(resp.status_code, 400)

    def test_create_promise_without_authentication(self):
        # setup
        promise_since = self.timezone.localize(datetime.now())
        promise_until = promise_since + timedelta(hours=1)

        # when
        resp = self.client.post('/promises/', data={
            'sinceWhen': iso8601(promise_since),
            'tilWhen': iso8601(promise_until),
            'user2': self.messi.id
        })

        # then
        self.assertEqual(resp.status_code, 403)

    def test_create_promise_with_readonly_properties(self):
        # setup
        promise_since = self.timezone.localize(datetime.now())
        promise_until = promise_since + timedelta(hours=1)
        created = self.timezone.localize(datetime(2018, 1, 1))
        explicit_id = 9999
        self.client.force_authenticate(user=self.ronaldo)

        # when
        resp = self.client.post('/promises/', data={
            'id': explicit_id,
            'created': created,
            'sinceWhen': iso8601(promise_since),
            'tilWhen': iso8601(promise_until),
            'user1': self.messi.id,
            'user2': self.neymar.id
        })

        # then
        self.assertEqual(resp.status_code, 201)
        self.assertFieldsNotEqual(resp.data,
                                  id=explicit_id,
                                  user1=self.messi.id,
                                  created=created)

    def test_update_promise(self):
        # setup
        promise_since = self.timezone.localize(datetime.now())
        promise_until = promise_since + timedelta(hours=1)
        self.client.force_authenticate(user=self.ronaldo)

        # when
        resp = self.client.put(f'/promises/{self.promise_ronaldo_messi.id}/', {
            'sinceWhen': iso8601(promise_since),
            'tilWhen': iso8601(promise_until),
        })

        # then
        self.assertEqual(resp.status_code, 200)
        self.assertFieldsEqual(resp.data,
                               sinceWhen=promise_since,
                               tilWhen=promise_until,
                               user2=self.messi.id)

    def test_update_promise_with_put(self):
        # setup
        promise_since = self.promise_ronaldo_messi.sinceWhen - timedelta(hours=1)
        self.client.force_authenticate(user=self.ronaldo)

        # when
        resp = self.client.put(f'/promises/{self.promise_ronaldo_messi.id}/', {
            'sinceWhen': iso8601(promise_since)
        })

        # then
        self.assertEqual(resp.status_code, 200)
        self.assertDateTimeEqual(resp.data['sinceWhen'], promise_since)

    def test_update_promise_with_invalid_timespan(self):
        # setup
        promise_since = self.timezone.localize(datetime.now())
        promise_until = promise_since - timedelta(seconds=1)
        self.client.force_authenticate(user=self.ronaldo)

        # when
        resp = self.client.put(f'/promises/{self.promise_ronaldo_messi.id}/', {
            'sinceWhen': iso8601(promise_since),
            'tilWhen': iso8601(promise_until)
        })

        # then
        self.assertEqual(resp.status_code, 400)

    def test_update_promise_of_others(self):
        # setup
        promise_id = self.promise_messi_neymar.id
        promise_since = self.timezone.localize(datetime.now())
        promise_until = promise_since + timedelta(hours=1)
        self.client.force_authenticate(user=self.ronaldo)

        # when
        resp = self.client.put(f'/promises/{promise_id}/', {
            'sinceWhen': iso8601(promise_since),
            'tilWhen': iso8601(promise_until)
        })

        # then
        self.assertEqual(resp.status_code, 403)

    def test_update_promise_with_readonly_properties_not_changed(self):
        # setup
        random_id = 9999
        created = self.timezone.localize(datetime.now())
        self.client.force_authenticate(user=self.ronaldo)

        # when
        resp = self.client.put(f'/promises/{self.promise_ronaldo_messi.id}/', {
            'id': random_id,
            'created': created,
            'user1': self.messi.id,
            'user2': self.neymar.id
        })

        # then
        self.assertEqual(resp.status_code, 200)
        self.assertFieldsNotEqual(resp.data,
                                  id=random_id,
                                  created=created,
                                  user1=self.messi.id,
                                  user2=self.neymar.id)

    def test_update_nonexisting_promise(self):
        # setup
        nonexisting_id = 9999
        self.client.force_authenticate(user=self.ronaldo)

        # when
        resp = self.client.put(f'/promises/{nonexisting_id}/', {
            'sinceWhen': iso8601(datetime.now()),
        })

        # then
        self.assertEqual(resp.status_code, 404)

    def test_delete_promise(self):
        # setup
        self.client.force_authenticate(user=self.ronaldo)

        # when
        resp = self.client.delete(f'/promises/{self.promise_ronaldo_messi.id}/')

        # then
        self.assertEqual(resp.status_code, 204)

    def test_delete_promise_of_others(self):
        # setup
        self.client.force_authenticate(user=self.ronaldo)

        # when
        resp = self.client.delete(f'/promises/{self.promise_messi_neymar.id}/')

        # then
        self.assertEqual(resp.status_code, 403)

    def test_delete_nonexisting_promise(self):
        # setup
        nonexisting_id = 9999
        self.client.force_authenticate(user=self.ronaldo)

        # when
        resp = self.client.delete(f'/promises/{nonexisting_id}/')

        # then
        self.assertEqual(resp.status_code, 404)


class TestUsers(TestCase, PromisesUtilMixins):
    def setUp(self):
        parzival = self.create_user('parzival')
        art3mis = self.create_user('art3mis')
        anorak = self.create_user('anorak')
        self.create_promises_between_users([parzival, art3mis, anorak])
        self.client = APIClient()

    def test_list_users(self):
        # when
        resp = self.client.get('/users/')

        # then
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 3)
        self.assertFieldsEqual(resp.data[0],
                               username='parzival',
                               promises_as_inviter=[
                                   self.promise_parzival_art3mis.id,
                                   self.promise_parzival_anorak.id
                               ],
                               promises_as_invitee=[
                                   self.promise_art3mis_parzival.id,
                                   self.promise_anorak_parzival.id
                               ])
        self.assertFieldsEqual(resp.data[1],
                               username='art3mis',
                               promises_as_inviter=[
                                   self.promise_art3mis_parzival.id,
                                   self.promise_art3mis_anorak.id
                               ],
                               promises_as_invitee=[
                                   self.promise_parzival_art3mis.id,
                                   self.promise_anorak_art3mis.id
                               ])
        self.assertFieldsEqual(resp.data[2],
                               username='anorak',
                               promises_as_inviter=[
                                   self.promise_anorak_parzival.id,
                                   self.promise_anorak_art3mis.id
                               ],
                               promises_as_invitee=[
                                   self.promise_parzival_anorak.id,
                                   self.promise_art3mis_anorak.id
                               ])

    def test_get_user(self):
        # when
        resp = self.client.get(f'/users/{self.art3mis.id}/')

        # then
        self.assertEqual(resp.status_code, 200)
        self.assertFieldsEqual(resp.data,
                               username='art3mis',
                               promises_as_inviter=[
                                   self.promise_art3mis_parzival.id,
                                   self.promise_art3mis_anorak.id
                               ],
                               promises_as_invitee=[
                                   self.promise_parzival_art3mis.id,
                                   self.promise_anorak_art3mis.id
                               ])

    def test_get_nonexisting_user(self):
        # setup
        nonexisting_id = 9999

        # when
        resp = self.client.get(f'/users/{nonexisting_id}/')

        # then
        self.assertEqual(resp.status_code, 404)


class TestUserAll(TestCase, PromisesUtilMixins):
    def setUp(self):
        parzival = self.create_user('parzival')
        art3mis = self.create_user('art3mis')
        anorak = self.create_user('anorak')
        self.create_promises_between_users([parzival, art3mis, anorak])
        self.client = APIClient()

    def test_list_userall(self):
        # when
        resp = self.client.get('/userall/')

        # then
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 3)
        self.assertFieldsEqual(resp.data[0],
                               username='parzival',
                               whole_promises=[
                                   self.promise_parzival_art3mis.id,
                                   self.promise_parzival_anorak.id,
                                   self.promise_art3mis_parzival.id,
                                   self.promise_anorak_parzival.id
                               ])
        self.assertFieldsEqual(resp.data[1],
                               username='art3mis',
                               whole_promises=[
                                   self.promise_art3mis_parzival.id,
                                   self.promise_art3mis_anorak.id,
                                   self.promise_parzival_art3mis.id,
                                   self.promise_anorak_art3mis.id
                               ])
        self.assertFieldsEqual(resp.data[2],
                               username='anorak',
                               whole_promises=[
                                   self.promise_anorak_parzival.id,
                                   self.promise_anorak_art3mis.id,
                                   self.promise_parzival_anorak.id,
                                   self.promise_art3mis_anorak.id
                               ])

    def test_get_userall(self):
        # when
        resp = self.client.get(f'/userall/{self.art3mis.id}/')

        # then
        self.assertEqual(resp.status_code, 200)
        self.assertFieldsEqual(resp.data,
                               username='art3mis',
                               whole_promises=[
                                   self.promise_art3mis_parzival.id,
                                   self.promise_art3mis_anorak.id,
                                   self.promise_parzival_art3mis.id,
                                   self.promise_anorak_art3mis.id
                               ])

    def test_get_nonexisting_userall(self):
        # setup
        nonexisting_id = 9999

        # when
        resp = self.client.get(f'/userall/{nonexisting_id}/')

        # then
        self.assertEqual(resp.status_code, 404)
