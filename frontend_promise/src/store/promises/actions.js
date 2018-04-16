export const TRY_LOGIN = "TRY_LOGIN";
export const tryLogin = (username, password) => {
	return {
		type: TRY_LOGIN,
		username: username,
		password: password
	};
};

export const ON_LOGIN_SUCCESS = "ON_LOGIN_SUCCESS";
export const onLoginSuccess = (users, username, userId, userToken, response) => {
	return {
		type: ON_LOGIN_SUCCESS,
		payload: {
			users: users,
			username: username,
			userId: userId,
			userToken: userToken,
			response: response
		}
	};
};

export const ADD_PROMISE_TO_SERVER = "ADD_PROMISE_TO_SERVER";
export const addPromiseToServer = (sinceWhen, tilWhen, user2Username, users, userToken) => {
	return {
		type: ADD_PROMISE_TO_SERVER,
		sinceWhen: sinceWhen,
		tilWhen: tilWhen,
		user2Username: user2Username,
		users: users,
		userToken: userToken
	};
};

export const ADD_PROMISE_AS_INVITER = "ADD_PROMISE_AS_INVITER";
export const addPromiseAsInviter = (promiseId) => {
	return {
		type: ADD_PROMISE_AS_INVITER,
		payload: {
			promiseId: promiseId
		}
	};
};

export const LOGOUT = "LOGOUT";
export const logOut = () => {
	return {
		type: LOGOUT
	};
};
