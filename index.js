'use strict';

const request = require('request');
const fs = require('fs');

const {
  ABC_APP_ID,
  ABC_APP_KEY,
  ABC_CLUB_NUMBER,
  ABC_API_URL,
} = process.env;


function makeRequest(resource, page, accumulator, done) {
  request.get(`${ABC_API_URL}/${ABC_CLUB_NUMBER}/${resource}`, {
    qs: { page },
    headers: {
      accept: 'application/json',
      app_id: ABC_APP_ID,
      app_key: ABC_APP_KEY,
    },
  }, (err, response, body) => {
    if (err) {
      console.log(err);
      return done(err);
    }

    const res = JSON.parse(body);

    const {
      status: {
        nextPage,
      },
      [resource]: data = [],
    } = res;

    accumulator.push(...data);

    if (nextPage) {
      return makeRequest(resource, nextPage, accumulator, done);
    }

    return done(null, accumulator)
  });
}

makeRequest('members', 1, [], (membersErr, members) => {
  if (membersErr) {
    return console.log(membersErr);
  }

  return makeRequest('prospects', 1, [], (prospectsErr, prospects) => {
    if (prospectsErr) {
      return console.log(prospectsErr);
    }

    fs.writeFileSync('members-and-prospects.json', JSON.stringify({ members, prospects }, null, 4), 'utf8');
  });
});
