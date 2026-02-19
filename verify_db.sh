#!/bin/bash
# MongoDB verification script

echo "======================================"
echo "MongoDB Database Verification"
echo "======================================"

mongosh --quiet octofit_db --eval "
print('\\n=== Collections in octofit_db ===');
db.getCollectionNames().forEach(function(collection) {
    print('  - ' + collection);
});

print('\\n=== Sample from users collection ===');
printjson(db.users.findOne());

print('\\n=== Sample from teams collection ===');
printjson(db.teams.findOne());

print('\\n=== Sample from activities collection ===');
printjson(db.activities.findOne());

print('\\n=== Sample from leaderboard collection ===');
printjson(db.leaderboard.findOne());

print('\\n=== Sample from workouts collection ===');
printjson(db.workouts.findOne());

print('\\n=== Collection Counts ===');
print('Users: ' + db.users.countDocuments({}));
print('Teams: ' + db.teams.countDocuments({}));
print('Activities: ' + db.activities.countDocuments({}));
print('Leaderboard: ' + db.leaderboard.countDocuments({}));
print('Workouts: ' + db.workouts.countDocuments({}));
"
