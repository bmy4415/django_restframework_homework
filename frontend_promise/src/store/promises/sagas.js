import { take, put, call, fork } from "redux-saga/effects";
import api from "services/api";
import * as actions from "./actions";

const usersUrl = "http://13.125.124.84:8000/users/";
const promisesUrl = "http://13.125.124.84:8000/promises/";

const findUserIdFromUsers = (username, users) => {
	if(!username || !users) return null;

	for(let i=0; i<users.length; i++) {
		if(users[i].username == username) return users[i].id;
	}

	return null;
};


export function* watchTryLogin() {
	while(true) {
		const { username, password } = yield take(actions.TRY_LOGIN);
		const users = yield call(api.get, usersUrl);
		const userId = findUserIdFromUsers(username, users);
		
		// if user does not exist, alert
		if(!userId) {
			alert(`There is no user: ${username}`);
			continue;
		}
		const userToken = new Buffer(`${username}:${password}`).toString('base64');
		const response = yield call(api.get, `${usersUrl}${userId}/`, {
			headers: {
				"Authorization": `Basic ${userToken}`
			}
		});

		if(response.error) {
			alert("login failed");
			continue;
		}

		yield put(actions.onLoginSuccess(users, username, userId, userToken, response));
			
	}
};

export function* watchAddPromiseToServer() {
	while(true) {
		const { sinceWhen, tilWhen, user2Username, users, userToken } = yield take(actions.ADD_PROMISE_TO_SERVER);
		const user2Id = findUserIdFromUsers(user2Username, users);
		const body = {
			sinceWhen: sinceWhen,
			tilWhen: tilWhen,
			user2: user2Id
		};
		const response = yield call(api.post, `${promisesUrl}`, body, {
			headers: {
				"Authorization": `Basic ${userToken}`,
				"Content-Type": "application/json"
			}
		});

		if(response.error) {
			alert("add promise failed");
			// console.log(response.error);
			continue;
		}
		// console.log(response);
		yield put(actions.addPromiseAsInviter(response.id));
	}
}

export default function* () {
	yield fork(watchTryLogin);
	yield fork(watchAddPromiseToServer);
};
