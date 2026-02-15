// server.js (backend)
const express = require('express');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid'); // optional, for unique IDs
const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

// In-memory storage for demo purposes
// Each endorsement now has: { id, name, role, relationship, linkedin, email, endorsement, linkedinProfilePic, status }
let endorsements = [];

// GET all endorsements (public endpoint only returns approved ones)
app.get('/api/endorsements', (req, res) => {
    const approvedEndorsements = endorsements.filter(e => e.status === 'approved');
    res.json(approvedEndorsements);
});

// GET all endorsements (admin view - all, including pending)
app.get('/api/admin/endorsements', (req, res) => {
    const adminKey = req.headers['x-admin-key'];
    if (!adminKey || adminKey !== process.env.ADMIN_KEY) {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    res.json(endorsements);
});

// POST a new endorsement (always starts as pending)
app.post('/api/endorsements', (req, res) => {
    const data = req.body;

    // Basic validation
    if (!data.name || !data.role || !data.relationship || !data.linkedin || !data.endorsement || !data.email) {
        return res.status(400).json({ error: 'All fields are required' });
    }

    const newEndorsement = {
        id: uuidv4(),
        name: data.name,
        role: data.role,
        relationship: data.relationship,
        linkedin: data.linkedin,
        email: data.email,
        endorsement: data.endorsement,
        linkedinProfilePic: '', // front-end can handle initials if empty
        status: 'pending' // important! starts as pending
    };

    endorsements.push(newEndorsement);

    res.status(201).json({ message: 'Endorsement submitted successfully and is pending review' });
});

// PUT endpoint to approve an endorsement (admin only)
app.put('/api/admin/endorsements/:id/approve', (req, res) => {
    const adminKey = req.headers['x-admin-key'];
    if (!adminKey || adminKey !== process.env.ADMIN_KEY) {
        return res.status(401).json({ error: 'Unauthorized' });
    }

    const { id } = req.params;
    const endorsement = endorsements.find(e => e.id === id);

    if (!endorsement) return res.status(404).json({ error: 'Endorsement not found' });

    endorsement.status = 'approved';
    res.json({ message: 'Endorsement approved', endorsement });
});

// DELETE an endorsement (admin only)
app.delete('/api/admin/endorsements/:id', (req, res) => {
    const adminKey = req.headers['x-admin-key'];
    if (!adminKey || adminKey !== process.env.ADMIN_KEY) {
        return res.status(401).json({ error: 'Unauthorized' });
    }

    const { id } = req.params;
    const index = endorsements.findIndex(e => e.id === id);

    if (index === -1) return res.status(404).json({ error: 'Endorsement not found' });

    endorsements.splice(index, 1);
    res.json({ message: 'Endorsement deleted', id });
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
