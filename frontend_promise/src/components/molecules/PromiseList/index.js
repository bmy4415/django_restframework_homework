import React, { PropTypes } from 'react'


const PromiseList = ({ response, username, userId }) => {
	return (
		<div>
			<h1>My name is {username}, My id is {userId}</h1>
			<h2>total {response.promises_as_inviter.length} promises_as_inviter are below</h2>
			{response.promises_as_inviter.map(t => 
				<h4 key={t}>{t}</h4>
			)}
			<h2>total {response.promises_as_invitee.length} promises_as_invitee are below</h2>
			{response.promises_as_invitee.map(t => 
				<h4 key={t}>{t}</h4>
			)}

		</div>
	);
}

PromiseList.propTypes = {
  // reverse: PropTypes.bool,
  // children: PropTypes.node,
}

export default PromiseList;
