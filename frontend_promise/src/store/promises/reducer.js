import { initialState } from "./selectors";
import * as actions from "./actions";

const promise_reducer = (state = initialState, action) => {
	switch(action.type) {
		case actions.ON_LOGIN_SUCCESS:
			return action.payload;

		case actions.ADD_PROMISE_AS_INVITER:
			return {
				...state,
				response: {
					promises_as_inviter: [...state.response.promises_as_inviter, action.payload.promiseId],
					promises_as_invitee: state.response.promises_as_invitee
				}
			};

		case actions.LOGOUT:
			return initialState;

		default:
			console.log("here is defaulttttttttttttttttttttttttttt");
			return state;
	}
};

export default promise_reducer;
