<?php

namespace App\Events;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class WeightReceived implements ShouldBroadcast
{
    use SerializesModels;

    public $weight;

    public function __construct($weight)
    {
        $this->weight = $weight;
    }

    public function broadcastOn()
    {
        return new Channel('weight-channel');
    }

    public function broadcastAs()
    {
        return 'weight-received';
    }
}

