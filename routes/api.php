<?php

use Illuminate\Http\Request;
use App\Events\WeightReceived;
use Illuminate\Support\Facades\Route;

use Illuminate\Support\Facades\Cache;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});





// Receive weight from Python
// Route::post('/receive-weight', function (Request $request) {
//     $weight = $request->input('weight');

//     if ($weight) {
//         Cache::put('latest_weight', $weight, 10); // store for 60 seconds
//         return response()->json(['status' => 'received', 'weight' => $weight]);
//     }

//     return response()->json(['status' => 'error', 'message' => 'No weight received'], 422);
// })->middleware('throttle:300,1');

Route::post('/receive-weight', function (Request $request) {
    $weight = $request->input('weight');

    if ($weight) {
        Cache::put('latest_weight', $weight, 10); // store for 10 seconds
        return response()->json(['status' => 'received', 'weight' => $weight]);
    }

    return response()->json(['status' => 'error', 'message' => 'No weight received'], 422);
});

use App\Models\WeightLog;

Route::post('/save-weight', function () {
    $weight = Cache::get('latest_weight');

    if ($weight) {
        WeightLog::create(['weight' => $weight]);
        return response()->json(['status' => 'success', 'message' => 'Weight saved.', 'weight' => $weight]);
    }

    return response()->json(['status' => 'error', 'message' => 'No weight to save.']);
});



// // Endpoint to fetch weight in browser
// Route::get('/latest-weight', function () {
//     return response()->json([
//         'weight' => Cache::get('latest_weight', '0.000')
//     ]);
// })->middleware('throttle:120,1');



