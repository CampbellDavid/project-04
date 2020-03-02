import React from 'react'
import axios from 'axios'
import { Link } from 'react-router-dom'
import Auth from '../../lib/auth'
import GroupCard from '../groups/GroupCard'

class EventDisplay extends React.Component {

  state = {
    event: null,
    groups: null,
    user: null
  }

  async componentDidMount() {
    try {
      const userId = Auth.getPayload().sub
      const eventId = this.props.match.params.id
      await axios.all([
        axios.get(`/api/events/${eventId}`),
        axios.get(`/api/events/${eventId}/event_groups`),
        Auth.getPayload() && axios.get(`/api/user/${userId}`)
      ])
        .then(axios.spread((eventRequest, groupsRequest, userRequest) => {
          this.setState({
            event: eventRequest.data,
            groups: groupsRequest.data,
            user: userRequest.data
          })
        }))
    } catch (error) {
      console.log(error)
    }
  }

  isOwner = () => {
    return Auth.getPayload().sub === this.state.event.owner.id
  }

  deleteEvent = async () => {
    const eventId = this.props.match.params.id
    try {
      await axios.delete(`/api/events/${eventId}/`, {
        headers: { Authorization: `Bearer ${Auth.getToken()}` }
      })
      this.props.history.push('/events')
    } catch (err) {
      this.props.history.push('/unknown-path')
    }
  }

  addToWishList = async () => {
    const userId = Auth.getPayload().sub
    const wishListArr = this.state.user.wish_list
    const currentEvent = this.state.event.id
    const eventId = this.state.event.id
    const index = wishListArr.indexOf(currentEvent)

    wishListArr.includes(eventId) ?
      wishListArr.splice(index, 1) :
      wishListArr.push(this.state.event.id)
    this.setState({ user: { wish_list: wishListArr } })
    console.log(this.state.user)
    try {
      await axios.put(`/api/user/${userId}`, this.state.user, {
        headers: { Authorization: `Bearer ${Auth.getToken()}` }
      })
    } catch (err) {
      console.log(err.response.data)
    }
  }

  render() {
    if (!this.state.event) return null
    const eventId = this.state.event.id
    const wishListArr = this.state.user.wish_list
    const filteredGroups = this.state.groups.filter(group => group.event.id === this.state.event.id)

    return (
      <>
        <div className="event-show">
          <h1>{this.state.event.title}</h1>
        </div>

        <div>
          <h3>Groups</h3>



          {filteredGroups.map(group => <GroupCard key={group.id} {...group} />)}
        </div>

        {Auth.isAuthenticated() ?
          <>
            <Link to={`/events/${eventId}/event_groups/create`}>
              <button type="button" className="button">Create New Group</button>
            </Link>

            {this.isOwner() &&
              <div>
                <Link to={`/events/${eventId}/amend`}>
                  <button className="button" type="button">Amend Event</button>
                </Link>
                <button className="button" onClick={this.deleteEvent}>Delete Event</button>
              </div>}

          </>
          : null}

        {Auth.isAuthenticated() ?
          wishListArr.includes(eventId) ?
            <button className="button" onClick={this.addToWishList}>Remove from Wishlist</button> :
            <button className="button" onClick={this.addToWishList}>Add to Wishlist</button>
          :
          null}
      </>
    )
  }
}

export default EventDisplay