<?php

namespace App\Providers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Foundation\Support\Providers\RouteServiceProvider as ServiceProvider;

class RouteServiceProvider extends ServiceProvider
{
    /**
     * The path to the "home" route for your application.
     *
     * Typically, users are redirected here after authentication.
     *
     * @var string
     */
    public const HOME = '/home';

    /**
     * Define your route model bindings, pattern filters, and other route configuration.
     */
    public function boot(): void
    {
        $this->configureRateLimiting();

        $this->routes(function () {
            Route::middleware('api')
                ->prefix('api')
                ->group(base_path('routes/api.php'));

            Route::middleware('web')
                ->group(base_path('routes/web.php'));
        });
         // ✅ Manually register this one GET route without throttle
        Route::get('/api/latest-weight', function () {
            return response()->json([
                'weight' => Cache::get('latest_weight', '0.000')
            ]);
        })->withoutMiddleware(['throttle', 'api']);
    }

    /**
     * Configure the rate limiters for the application.
     */
    protected function configureRateLimiting(): void
    {
        // RateLimiter::for('api', function (Request $request) {
        //     return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
        // });

        RateLimiter::for('api', function (Request $request) {
        // ✅ Allow unlimited requests to /api/latest-weight
        if ($request->is('api/latest-weight')) {
            return Limit::none();
        }
        if ($request->is('api/receive-weight')) {
            return Limit::none();
        }

        // ✅ Default limit for all other API routes
        // return Limit::perMinute(60)->by($request->ip());
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
        });

        
    }
}
