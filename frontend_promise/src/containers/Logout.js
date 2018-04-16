import { connect } from "react-redux";
import Logout from "../components/molecules/Logout";
import { logOut } from "../store/promises/actions";


const mapStateToProps = (state) => {
	return {
		statefunction: state
	};
};

const mapDispatchToProps = (dispatch) => {
	return {
		onClickTodo: () => {
			dispatch(logOut());
		}
	};
};

export default connect(mapStateToProps, mapDispatchToProps)(Logout);
