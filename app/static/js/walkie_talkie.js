const socket = io("http://localhost:8000", {
    transports: ['websocket'],
    path: "/socket.io/"
});

let localStream = null;
let peerConnections = {};
let roomId = "walkie-room";  // default room to keep it simple


async function startWalkieTalkie() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    console.log("🎙️ Microphone access granted");

    // Add track to peer connection
    stream.getTracks().forEach((track) => {
        console.log("🎧 Adding track:", track);
        pc.addTrack(track, stream);
    });

    // Play local audio if needed
    const localAudio = new Audio();
    localAudio.srcObject = stream;
    localAudio.play();
}
// 🔊 Ask for microphone access and prepare stream
async function initMedia() {
    try {
        localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        console.log("🎙️ Microphone access granted");

        socket.emit("join_room", { room: roomId });

    } catch (err) {
        console.error("🚫 Microphone access denied:", err);
    }
}

// 📞 Handle offer from another peer
socket.on("offer", async ({ from, offer }) => {
    const pc = createPeerConnection(from);
    await pc.setRemoteDescription(new RTCSessionDescription(offer));

    const answer = await pc.createAnswer();
    await pc.setLocalDescription(answer);

    socket.emit("answer", {
        to: from,
        answer: pc.localDescription
    });
});

// ✅ Handle answer from another peer
socket.on("answer", async ({ from, answer }) => {
    await peerConnections[from].setRemoteDescription(new RTCSessionDescription(answer));
});

// 🔁 ICE candidate exchange
socket.on("ice-candidate", ({ from, candidate }) => {
    if (peerConnections[from]) {
        peerConnections[from].addIceCandidate(new RTCIceCandidate(candidate));
    }
});

// 👥 New user joins
socket.on("user_joined", async ({ sid }) => {
    const pc = createPeerConnection(sid);

    // Add our audio stream
    localStream.getTracks().forEach(track => pc.addTrack(track, localStream));

    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);

    socket.emit("offer", {
        to: sid,
        offer: pc.localDescription
    });
});

// 📶 Peer connection factory
function createPeerConnection(sid) {
    const pc = new RTCPeerConnection();

    pc.onicecandidate = (event) => {
        if (event.candidate) {
            socket.emit("ice-candidate", {
                to: sid,
                candidate: event.candidate
            });
        }
    };

    pc.ontrack = (event) => {
    console.log("🔊 Received remote track");
    const remoteAudio = new Audio();
    remoteAudio.srcObject = event.streams[0];
    remoteAudio.play().then(() => {
        console.log("🔊 Remote audio playing");
    }).catch(err => console.error("Audio play error:", err));
};

    peerConnections[sid] = pc;
    return pc;
}

// 📢 Start
initMedia();
