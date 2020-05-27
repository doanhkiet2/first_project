import React from 'react'


export function UserLink(props) {
    const { username } = props
    console.log(props.children)
    const handleUserLink = (event) => {
        window.location.href = `/profiles/${username}`
    }
    //some where wrap me
    return <span className="pointer" onClick={handleUserLink}>
        {props.children}
    </span>
}

export function UserDisplay(props) {
    const { user, includeFullName } = props
    const nameDisplay = includeFullName === true ? `${user.first_name} ${user.last_name}` : ""

    return <React.Fragment>
        {nameDisplay}
        <UserLink username={user.username}>@{user.username}</UserLink>
    </React.Fragment>
}


export function UserPicture(props) {
    const { user } = props
    return <UserLink username={user.username}><span className='px-3 py-2 rounded-circle bg-dark text-white '>
        {user.username[0]}
    </span>
    </UserLink>
}
